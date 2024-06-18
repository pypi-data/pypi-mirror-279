#!/usr/bin/env python3
"""Communicate with Volkswagen Connect services."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
import hashlib
from json import dumps as to_json
import logging
from random import randint, random
import re
from urllib.parse import parse_qs, urljoin, urlparse

from aiohttp import ClientTimeout, client_exceptions
from aiohttp.hdrs import METH_GET, METH_POST, METH_PUT
from bs4 import BeautifulSoup
import jwt

from .vw_const import (
    APP_URI,
    BASE_API,
    BASE_AUTH,
    BASE_SESSION,
    BRAND,
    CLIENT,
    COUNTRY,
    HEADERS_AUTH,
    HEADERS_SESSION,
    USER_AGENT,
)
from .vw_utilities import json_loads
from .vw_vehicle import Vehicle

MAX_RETRIES_ON_RATE_LIMIT = 3

_LOGGER = logging.getLogger(__name__)  # pylint: disable=unreachable

TIMEOUT = timedelta(seconds=30)
JWT_ALGORITHMS = ["RS256"]


# noinspection PyPep8Naming
class Connection:
    """Connection to VW-Group Connect services."""

    _login_lock = asyncio.Lock()

    # Init connection class
    def __init__(
        self,
        session,
        username,
        password,
        fulldebug=False,
        country=COUNTRY,
        interval=timedelta(minutes=5),
    ) -> None:
        """Initialize."""
        self._x_client_id = None
        self._session = session
        self._session_fulldebug = fulldebug
        self._session_headers = HEADERS_SESSION.copy()
        self._session_base = BASE_SESSION
        self._session_auth_headers = HEADERS_AUTH.copy()
        self._session_auth_base = BASE_AUTH
        self._session_refresh_interval = interval

        no_vin_key = ""
        self._session_auth_ref_urls = {no_vin_key: BASE_SESSION}
        self._session_spin_ref_urls = {no_vin_key: BASE_SESSION}
        self._session_logged_in = False
        self._session_first_update = False
        self._session_auth_username = username
        self._session_auth_password = password
        self._session_tokens = {}
        self._session_country = country.upper()

        self._vehicles = []

        _LOGGER.debug("Using service %s", self._session_base)

        self._jarCookie = ""
        self._state = {}

        self._service_status = {}

    def _clear_cookies(self):
        self._session._cookie_jar._cookies.clear()  # pylint: disable=protected-access

    # API Login
    async def doLogin(self, tries: int = 1):
        """Login method, clean login."""
        async with self._login_lock:
            _LOGGER.debug("Initiating new login")

            for i in range(tries):
                self._session_logged_in = await self._login("Legacy")
                if self._session_logged_in:
                    break
                if i > tries:
                    _LOGGER.error("Login failed after %s tries", tries)
                    return False
                await asyncio.sleep(random() * 5)

            if not self._session_logged_in:
                return False

            _LOGGER.info("Successfully logged in")
            self._session_tokens["identity"] = self._session_tokens["Legacy"].copy()

            # Get list of vehicles from account
            _LOGGER.debug("Fetching vehicles associated with account")
            self._session_headers.pop("Content-Type", None)
            loaded_vehicles = await self.get(url=f"{BASE_API}/vehicle/v2/vehicles")
            # Add Vehicle class object for all VIN-numbers from account
            if loaded_vehicles.get("data") is not None:
                _LOGGER.debug("Found vehicle(s) associated with account")
                self._vehicles = []
                for vehicle in loaded_vehicles.get("data"):
                    self._vehicles.append(Vehicle(self, vehicle.get("vin")))
            else:
                _LOGGER.warning("Failed to login to Volkswagen Connect API")
                self._session_logged_in = False
                return False

            # Update all vehicles data before returning
            await self.update()
            return True

    async def get_openid_config(self):
        """Get OpenID config."""
        if self._session_fulldebug:
            _LOGGER.debug("Requesting openid config")
        req = await self._session.get(
            url=f"{BASE_API}/login/v1/idk/openid-configuration"
        )
        if req.status != 200:
            _LOGGER.error("Failed to get OpenID configuration, status: %s", req.status)
            raise Exception("OpenID configuration error")  # pylint: disable=broad-exception-raised
        return await req.json()

    async def get_authorization_page(self, authorization_endpoint, client):
        """Get authorization page (login page)."""
        # https://identity.vwgroup.io/oidc/v1/authorize?nonce={NONCE}&state={STATE}&response_type={TOKEN_TYPES}&scope={SCOPE}&redirect_uri={APP_URI}&client_id={CLIENT_ID}
        # https://identity.vwgroup.io/oidc/v1/authorize?client_id={CLIENT_ID}&scope={SCOPE}&response_type={TOKEN_TYPES}&redirect_uri={APP_URI}
        if self._session_fulldebug:
            _LOGGER.debug(
                'Requesting authorization page from "%s"', authorization_endpoint
            )
            self._session_auth_headers.pop("Referer", None)
            self._session_auth_headers.pop("Origin", None)
            _LOGGER.debug('Request headers: "%s"', self._session_auth_headers)

        try:
            req = await self._session.get(
                url=authorization_endpoint,
                headers=self._session_auth_headers,
                allow_redirects=False,
                params={
                    "redirect_uri": APP_URI,
                    "response_type": CLIENT[client].get("TOKEN_TYPES"),
                    "client_id": CLIENT[client].get("CLIENT_ID"),
                    "scope": CLIENT[client].get("SCOPE"),
                },
            )

            # Check if the response contains a redirect location
            location = req.headers.get("Location")
            if not location:
                # pylint: disable=broad-exception-raised
                raise Exception(
                    f"Missing 'Location' header, payload returned: {await req.content.read()}"
                )

            ref = urljoin(authorization_endpoint, location)
            if "error" in ref:
                parsed_query = parse_qs(urlparse(ref).query)
                error_msg = parsed_query.get("error", ["Unknown error"])[0]
                error_description = parsed_query.get(
                    "error_description", ["No description"]
                )[0]
                _LOGGER.info("Authorization error: %s", error_description)
                raise Exception(error_msg)  # pylint: disable=broad-exception-raised

            # If redirected, fetch the new location
            req = await self._session.get(
                url=ref, headers=self._session_auth_headers, allow_redirects=False
            )

            if req.status != 200:
                raise Exception("Failed to fetch authorization endpoint")  # pylint: disable=broad-exception-raised

            return await req.text()

        except Exception as e:
            _LOGGER.warning("Error during fetching authorization page: %s", str(e))
            raise

    def extract_form_data(self, page_content, form_id):
        """Extract form data from a page."""
        soup = BeautifulSoup(page_content, "html.parser")
        form = soup.find("form", id=form_id)
        if form is None:
            raise Exception(f"Form with ID '{form_id}' not found.")  # pylint: disable=broad-exception-raised
        return {
            input_field["name"]: input_field["value"]
            for input_field in form.find_all("input", type="hidden")
        }

    def extract_password_form_data(self, soup):
        """Extract password form data from a page."""
        pw_form = {}
        for script in soup.find_all("script"):
            if "src" in script.attrs or not script.string:
                continue
            script_text = script.string

            if "window._IDK" not in script_text:
                continue  # Skip scripts that don't contain relevant data
            if re.match('"errorCode":"', script_text):
                raise Exception("Error code found in script data.")  # pylint: disable=broad-exception-raised

            pw_form["relayState"] = re.search(
                '"relayState":"([a-f0-9]*)"', script_text
            )[1]
            pw_form["hmac"] = re.search('"hmac":"([a-f0-9]*)"', script_text)[1]
            pw_form["email"] = re.search('"email":"([^"]*)"', script_text)[1]
            pw_form["_csrf"] = re.search("csrf_token:\\s*'([^\"']*)'", script_text)[1]

            post_action = re.search('"postAction":\\s*"([^"\']*)"', script_text)[1]
            client_id = re.search('"clientId":\\s*"([^"\']*)"', script_text)[1]
            return pw_form, post_action, client_id

        raise Exception("Password form data not found in script.")  # pylint: disable=broad-exception-raised

    async def post_form(self, session, url, headers, form_data, redirect=True):
        """Post a form and check for success."""
        req = await session.post(
            url, headers=headers, data=form_data, allow_redirects=redirect
        )
        if not redirect and req.status == 302:
            return req.headers["Location"]
        if req.status != 200:
            raise Exception("Form POST request failed.")  # pylint: disable=broad-exception-raised
        return await req.text()

    async def handle_login_with_password(self, session, url, auth_headers, form_data):
        """Handle login with email and password."""
        return await self.post_form(session, url, auth_headers, form_data, False)

    async def follow_redirects(self, session, pw_url, redirect_location):
        """Handle redirects."""
        ref = urljoin(pw_url, redirect_location)
        max_depth = 10
        while not ref.startswith(APP_URI):
            if max_depth == 0:
                raise Exception("Too many redirects")  # pylint: disable=broad-exception-raised
            response = await session.get(
                url=ref, headers=self._session_auth_headers, allow_redirects=False
            )
            if "Location" not in response.headers:
                _LOGGER.warning("Failed to find next redirect location")
                raise Exception("Redirect error")  # pylint: disable=broad-exception-raised
            ref = urljoin(ref, response.headers["Location"])
            max_depth -= 1
        return ref

    async def _login(self, client="Legacy"):
        """Login function."""

        try:
            # Clear cookies and reset headers
            self._clear_cookies()
            self._session_headers = HEADERS_SESSION.copy()
            self._session_auth_headers = HEADERS_AUTH.copy()

            # Get OpenID configuration
            openid_config = await self.get_openid_config()
            authorization_endpoint = openid_config["authorization_endpoint"]
            token_endpoint = openid_config["token_endpoint"]
            auth_issuer = openid_config["issuer"]

            # Get authorization page
            authorization_page = await self.get_authorization_page(
                authorization_endpoint, client
            )

            # Extract form data
            mailform = self.extract_form_data(authorization_page, "emailPasswordForm")
            mailform["email"] = self._session_auth_username
            pe_url = auth_issuer + BeautifulSoup(
                authorization_page, "html.parser"
            ).find("form", id="emailPasswordForm").get("action")

            # POST email
            # https://identity.vwgroup.io/signin-service/v1/{CLIENT_ID}/login/identifier
            self._session_auth_headers["Referer"] = authorization_endpoint
            self._session_auth_headers["Origin"] = auth_issuer
            response_text = await self.post_form(
                self._session, pe_url, self._session_auth_headers, mailform
            )

            # Extract password form data
            response_soup = BeautifulSoup(response_text, "html.parser")
            pw_form, post_action, client_id = self.extract_password_form_data(
                response_soup
            )

            # Add password to form data
            pw_form["password"] = self._session_auth_password
            pw_url = f"{auth_issuer}/signin-service/v1/{client_id}/{post_action}"

            # POST password
            self._session_auth_headers["Referer"] = pe_url
            redirect_location = await self.handle_login_with_password(
                self._session, pw_url, self._session_auth_headers, pw_form
            )

            # Handle redirects and extract tokens
            redirect_response = await self.follow_redirects(
                self._session, pw_url, redirect_location
            )
            jwt_auth_code = parse_qs(urlparse(redirect_response).query)["code"][0]

            # Exchange authorization code for tokens
            token_body = {
                "client_id": CLIENT[client].get("CLIENT_ID"),
                "grant_type": "authorization_code",
                "code": jwt_auth_code,
                "redirect_uri": APP_URI,
            }

            # Token endpoint
            token_response = await self.post_form(
                self._session, token_endpoint, self._session_auth_headers, token_body
            )

            # Store session tokens
            self._session_tokens[client] = json_loads(token_response)

            # Verify tokens
            if not await self.verify_tokens(
                self._session_tokens[client].get("id_token", ""), "identity"
            ):
                _LOGGER.warning("User identity token could not be verified!")
            else:
                _LOGGER.debug("User identity token verified successfully")

            # Mark session as logged in
            self._session_logged_in = True

        except Exception as error:  # pylint: disable=broad-exception-caught
            _LOGGER.error("Login failed: %s", error)
            self._session_logged_in = False
            return False
        self._session_headers["Authorization"] = (
            "Bearer " + self._session_tokens[client]["access_token"]
        )
        return True

    async def _handle_action_result(self, response_raw):
        response = await response_raw.json(loads=json_loads)
        if not response:
            raise Exception("Invalid or no response")  # pylint: disable=broad-exception-raised
        if response == 429:
            return {"id": None, "state": "Throttled"}
        request_id = response.get("data", {}).get("requestID", 0)
        _LOGGER.debug("Request returned with request id: %s", request_id)
        return {"id": str(request_id)}

    async def terminate(self):
        """Log out from connect services."""
        _LOGGER.info("Initiating logout")
        await self.logout()

    async def logout(self):
        """Logout, revoke tokens."""
        self._session_headers.pop("Authorization", None)

        if self._session_logged_in:
            if self._session_headers.get("identity", {}).get("identity_token"):
                _LOGGER.info("Revoking Identity Access Token")

            if self._session_headers.get("identity", {}).get("refresh_token"):
                _LOGGER.info("Revoking Identity Refresh Token")
                params = {"token": self._session_tokens["identity"]["refresh_token"]}
                await self.post(
                    "https://emea.bff.cariad.digital/login/v1/idk/revoke", data=params
                )

    # HTTP methods to API
    async def _request(self, method, url, return_raw=False, **kwargs):
        """Perform a query to the VW-Group API."""
        _LOGGER.debug('HTTP %s "%s"', method, url)
        if kwargs.get("json", None):
            _LOGGER.debug("Request payload: %s", kwargs.get("json", None))
        try:
            async with self._session.request(
                method,
                url,
                headers=self._session_headers,
                timeout=ClientTimeout(total=TIMEOUT.seconds),
                cookies=self._jarCookie,
                raise_for_status=False,
                **kwargs,
            ) as response:
                response.raise_for_status()

                # Update cookie jar
                if self._jarCookie != "":
                    self._jarCookie.update(response.cookies)
                else:
                    self._jarCookie = response.cookies

                # Update service status
                await self.update_service_status(url, response.status)

                try:
                    if response.status == 204:
                        if return_raw:
                            res = response
                        else:
                            res = {"status_code": response.status}
                    elif response.status >= 200 or response.status <= 300:
                        res = await response.json(loads=json_loads)
                    else:
                        res = {}
                        _LOGGER.debug(
                            "Not success status code [%s] response: %s",
                            response.status,
                            response.text,
                        )
                except Exception:  # pylint: disable=broad-exception-caught
                    res = {}
                    _LOGGER.debug(
                        "Something went wrong [%s] response: %s",
                        response.status,
                        response.text,
                    )
                    if return_raw:
                        return response
                    return res

                if self._session_fulldebug:
                    _LOGGER.debug(
                        'Request for "%s" returned with status code [%s], headers: %s, response: %s',
                        url,
                        response.status,
                        response.headers,
                        res,
                    )
                else:
                    _LOGGER.debug(
                        'Request for "%s" returned with status code [%s]',
                        url,
                        response.status,
                    )

                if return_raw:
                    res = response
                return res
        except client_exceptions.ClientResponseError as httperror:
            # Update service status
            await self.update_service_status(url, httperror.code)
            raise httperror from None
        except Exception as error:
            # Update service status
            await self.update_service_status(url, 1000)
            raise error from None

    async def get(self, url, vin="", tries=0):
        """Perform a get query."""
        try:
            return await self._request(METH_GET, url)
        except client_exceptions.ClientResponseError as error:
            if error.status == 400:
                _LOGGER.error(
                    'Got HTTP 400 "Bad Request" from server, this request might be malformed or not implemented'
                    " correctly for this vehicle"
                )
            elif error.status == 401:
                _LOGGER.warning(
                    'Received "unauthorized" error while fetching data: %s', error
                )
                self._session_logged_in = False
            elif error.status == 429 and tries < MAX_RETRIES_ON_RATE_LIMIT:
                delay = randint(1, 3 + tries * 2)
                _LOGGER.debug(
                    "Server side throttled. Waiting %s, try %s", delay, tries + 1
                )
                await asyncio.sleep(delay)
                return await self.get(url, vin, tries + 1)
            elif error.status == 500:
                _LOGGER.info(
                    "Got HTTP 500 from server, service might be temporarily unavailable"
                )
            elif error.status == 502:
                _LOGGER.info(
                    "Got HTTP 502 from server, this request might not be supported for this vehicle"
                )
            else:
                _LOGGER.error("Got unhandled error from server: %s", error.status)
            return {"status_code": error.status}

    async def post(self, url, vin="", tries=0, return_raw=False, **data):
        """Perform a post query."""
        try:
            if data:
                return await self._request(
                    METH_POST, url, return_raw=return_raw, **data
                )
            return await self._request(METH_POST, url, return_raw=return_raw)
        except client_exceptions.ClientResponseError as error:
            if error.status == 429 and tries < MAX_RETRIES_ON_RATE_LIMIT:
                delay = randint(1, 3 + tries * 2)
                _LOGGER.debug(
                    "Server side throttled. Waiting %s, try %s", delay, tries + 1
                )
                await asyncio.sleep(delay)
                return await self.post(
                    url, vin, tries + 1, return_raw=return_raw, **data
                )
            raise

    async def put(self, url, vin="", tries=0, return_raw=False, **data):
        """Perform a put query."""
        try:
            if data:
                return await self._request(METH_PUT, url, return_raw=return_raw, **data)
            return await self._request(METH_PUT, url, return_raw=return_raw)
        except client_exceptions.ClientResponseError as error:
            if error.status == 429 and tries < MAX_RETRIES_ON_RATE_LIMIT:
                delay = randint(1, 3 + tries * 2)
                _LOGGER.debug(
                    "Server side throttled. Waiting %s, try %s", delay, tries + 1
                )
                await asyncio.sleep(delay)
                return await self.put(
                    url, vin, tries + 1, return_raw=return_raw, **data
                )
            raise

    # Update data for all Vehicles
    async def update(self):
        """Update status."""
        if not self.logged_in:
            if not await self._login():
                _LOGGER.warning("Login for %s account failed!", BRAND)
                return False
        try:
            if not await self.validate_tokens:
                _LOGGER.info(
                    "Session expired. Initiating new login for %s account", BRAND
                )
                if not await self.doLogin():
                    _LOGGER.warning("Login for %s account failed!", BRAND)
                    raise Exception(f"Login for {BRAND} account failed")  # pylint: disable=broad-exception-raised
            else:
                _LOGGER.debug("Going to call vehicle updates")
                # Get all Vehicle objects and update in parallell
                updatelist = [vehicle.update() for vehicle in self.vehicles]
                # Wait for all data updates to complete
                await asyncio.gather(*updatelist)

                return True
        except (OSError, LookupError, Exception) as error:  # pylint: disable=broad-exception-caught
            _LOGGER.warning("Could not update information: %s", error)
        return False

    async def getPendingRequests(self, vin):
        """Get status information for pending requests."""
        if not await self.validate_tokens:
            return False
        try:
            response = await self.get(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/pendingrequests"
            )

            if response:
                response["refreshTimestamp"] = datetime.now(UTC)
                return response

        except Exception as error:  # pylint: disable=broad-exception-caught
            _LOGGER.warning(
                "Could not fetch information for pending requests, error: %s", error
            )
        return False

    async def getOperationList(self, vin):
        """Collect operationlist for VIN, supported/licensed functions."""
        if not await self.validate_tokens:
            return False
        try:
            response = await self.get(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/capabilities", ""
            )
            if response.get("capabilities", False):
                data = response
            elif response.get("status_code", {}):
                _LOGGER.warning(
                    "Could not fetch operation list, HTTP status code: %s",
                    response.get("status_code"),
                )
                data = response
            else:
                _LOGGER.info("Could not fetch operation list: %s", response)
                data = {"error": "unknown"}
        except Exception as error:  # pylint: disable=broad-exception-caught
            _LOGGER.warning("Could not fetch operation list, error: %s", error)
            data = {"error": "unknown"}
        return data

    async def getSelectiveStatus(self, vin, services):
        """Get status information for specified services."""
        if not await self.validate_tokens:
            return False
        try:
            response = await self.get(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/selectivestatus?jobs={','.join(services)}",
                "",
            )

            for service in services:
                if not response.get(service):
                    _LOGGER.debug(
                        "Did not receive return data for requested service %s. (This is expected for several service/car combinations)",
                        service,
                    )

            if response:
                response.update({"refreshTimestamp": datetime.now(UTC)})
                return response

        except Exception as error:  # pylint: disable=broad-exception-caught
            _LOGGER.warning("Could not fetch selectivestatus, error: %s", error)
        return False

    async def getVehicleData(self, vin):
        """Get car information like VIN, nickname, etc."""
        if not await self.validate_tokens:
            return False
        try:
            response = await self.get(f"{BASE_API}/vehicle/v2/vehicles", "")

            for vehicle in response.get("data"):
                if vehicle.get("vin") == vin:
                    return {"vehicle": vehicle}

            _LOGGER.warning("Could not fetch vehicle data for vin %s", vin)

        except Exception as error:  # pylint: disable=broad-exception-caught
            _LOGGER.warning("Could not fetch vehicle data, error: %s", error)
        return False

    async def getParkingPosition(self, vin):
        """Get information about the parking position."""
        if not await self.validate_tokens:
            return False
        try:
            response = await self.get(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/parkingposition", ""
            )

            if "data" in response:
                return {"isMoving": False, "parkingposition": response["data"]}
            if response.get("status_code", {}):
                if response.get("status_code", 0) == 204:
                    _LOGGER.debug(
                        "Seems car is moving, HTTP 204 received from parkingposition"
                    )
                    return {"isMoving": True, "parkingposition": {}}

                _LOGGER.warning(
                    "Could not fetch parkingposition, HTTP status code: %s",
                    response.get("status_code"),
                )
            else:
                _LOGGER.info(
                    "Unhandled error while trying to fetch parkingposition data"
                )
        except Exception as error:  # pylint: disable=broad-exception-caught
            _LOGGER.warning("Could not fetch parkingposition, error: %s", error)
        return False

    async def getTripLast(self, vin):
        """Get car information like VIN, nickname, etc."""
        if not await self.validate_tokens:
            return False
        try:
            response = await self.get(
                f"{BASE_API}/vehicle/v1/trips/{vin}/shortterm/last", ""
            )
            if "data" in response:
                return {"trip_last": response["data"]}

            _LOGGER.warning(
                "Could not fetch last trip data, server response: %s", response
            )

        except Exception as error:  # pylint: disable=broad-exception-caught
            _LOGGER.warning("Could not fetch last trip data, error: %s", error)
        return False

    async def wakeUpVehicle(self, vin):
        """Wake up vehicle to send updated data to VW Backend."""
        if not await self.validate_tokens:
            return False
        try:
            return await self.post(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/vehiclewakeuptrigger",
                json={},
                return_raw=True,
            )

        except Exception as error:  # pylint: disable=broad-exception-caught
            _LOGGER.warning("Could not refresh the data, error: %s", error)
        return False

    async def get_request_status(self, vin, requestId, actionId=""):
        """Return status of a request ID for a given section ID."""
        if self.logged_in is False:
            if not await self.doLogin():
                _LOGGER.warning("Login for %s account failed!", BRAND)
                raise Exception(f"Login for {BRAND} account failed")  # pylint: disable=broad-exception-raised
        try:
            if not await self.validate_tokens:
                _LOGGER.info(
                    "Session expired. Initiating new login for %s account", BRAND
                )
                if not await self.doLogin():
                    _LOGGER.warning("Login for %s account failed!", BRAND)
                    raise Exception(f"Login for {BRAND} account failed")  # pylint: disable=broad-exception-raised

            response = await self.getPendingRequests(vin)

            requests = response.get("data", [])
            result = None
            for request in requests:
                if request.get("id", "") == requestId:
                    result = request.get("status")

            # Translate status messages to meaningful info
            if result in ("in_progress", "queued", "fetched"):
                status = "In Progress"
            elif result in ("request_fail", "failed"):
                status = "Failed"
            elif result == "unfetched":
                status = "No response"
            elif result in ("request_successful", "successful"):
                status = "Success"
            elif result == "fail_ignition_on":
                status = "Failed because ignition is on"
            else:
                status = result
        except Exception as error:
            _LOGGER.warning("Failure during get request status: %s", error)
            raise Exception(f"Failure during get request status: {error}") from error  # pylint: disable=broad-exception-raised
        else:
            return status

    async def check_spin_state(self):
        """Determine SPIN state to prevent lockout due to wrong SPIN."""
        result = await self.get(f"{BASE_API}/vehicle/v1/spin/state")
        remainingTries = result.get("remainingTries", None)
        if remainingTries is None:
            raise Exception("Couldn't determine S-PIN state.")  # pylint: disable=broad-exception-raised

        if remainingTries < 3:
            # pylint: disable=broad-exception-raised
            raise Exception(
                "Remaining tries for S-PIN is < 3. Bailing out for security reasons. "
                "To resume operation, please make sure the correct S-PIN has been set in the integration "
                "and then use the correct S-PIN once via the Volkswagen app."
            )

        return True

    async def setClimater(self, vin, data, action):
        """Execute climatisation actions."""
        action = "start" if action else "stop"
        try:
            response_raw = await self.post(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/climatisation/{action}",
                json=data,
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setClimater") from e  # pylint: disable=broad-exception-raised

    async def setClimaterSettings(self, vin, data):
        """Execute climatisation settings."""
        try:
            response_raw = await self.put(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/climatisation/settings",
                json=data,
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setClimaterSettings") from e  # pylint: disable=broad-exception-raised

    async def setAuxiliary(self, vin, data, action):
        """Execute auxiliary climatisation actions."""
        action = "start" if action else "stop"
        try:
            response_raw = await self.post(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/auxiliaryheating/{action}",
                json=data,
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setAuxiliary") from e  # pylint: disable=broad-exception-raised

    async def setWindowHeater(self, vin, action):
        """Execute window heating actions."""
        action = "start" if action else "stop"
        try:
            response_raw = await self.post(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/windowheating/{action}",
                json={},
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setWindowHeater") from e  # pylint: disable=broad-exception-raised

    async def setCharging(self, vin, action):
        """Execute charging actions."""
        action = "start" if action else "stop"
        try:
            response_raw = await self.post(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/charging/{action}",
                json={},
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setCharging") from e  # pylint: disable=broad-exception-raised

    async def setChargingSettings(self, vin, data):
        """Execute charging actions."""
        try:
            response_raw = await self.put(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/charging/settings",
                json=data,
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setChargingSettings") from e  # pylint: disable=broad-exception-raised

    async def setChargingCareModeSettings(self, vin, data):
        """Execute battery care mode actions."""
        try:
            response_raw = await self.put(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/charging/care/settings",
                json=data,
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setChargingCareModeSettings") from e  # pylint: disable=broad-exception-raised

    async def setReadinessBatterySupport(self, vin, data):
        """Execute readiness battery support actions."""
        try:
            response_raw = await self.put(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/readiness/batterysupport",
                json=data,
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setReadinessBatterySupport") from e  # pylint: disable=broad-exception-raised

    async def setDepartureProfiles(self, vin, data):
        """Execute departure timers actions."""
        try:
            response_raw = await self.put(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/departure/profiles",
                json=data,
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setDepartureProfiles") from e  # pylint: disable=broad-exception-raised

    async def setClimatisationTimers(self, vin, data):
        """Execute climatisation timers actions."""
        try:
            response_raw = await self.put(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/climatisation/timers",
                json=data,
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setClimatisationTimers") from e  # pylint: disable=broad-exception-raised

    async def setAuxiliaryHeatingTimers(self, vin, data):
        """Execute auxiliary heating timers actions."""
        try:
            response_raw = await self.put(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/auxiliaryheating/timers",
                json=data,
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setAuxiliaryHeatingTimers") from e  # pylint: disable=broad-exception-raised

    async def setDepartureTimers(self, vin, data):
        """Execute departure timers actions."""
        try:
            response_raw = await self.put(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/departure/timers",
                json=data,
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setDepartureTimers") from e  # pylint: disable=broad-exception-raised

    async def setLock(self, vin, lock, spin):
        """Remote lock and unlock actions."""
        await self.check_spin_state()
        action = "lock" if lock else "unlock"
        try:
            response_raw = await self.post(
                f"{BASE_API}/vehicle/v1/vehicles/{vin}/access/{action}",
                json={"spin": spin},
                return_raw=True,
            )
            return await self._handle_action_result(response_raw)
        except Exception as e:
            raise Exception("Unknown error during setLock") from e  # pylint: disable=broad-exception-raised

    # Token handling #
    @property
    async def validate_tokens(self):
        """Validate expiry of tokens."""
        idtoken = self._session_tokens["identity"]["id_token"]
        atoken = self._session_tokens["identity"]["access_token"]
        id_exp = jwt.decode(
            idtoken,
            options={"verify_signature": False, "verify_aud": False},
            algorithms=JWT_ALGORITHMS,
        ).get("exp", None)
        at_exp = jwt.decode(
            atoken,
            options={"verify_signature": False, "verify_aud": False},
            algorithms=JWT_ALGORITHMS,
        ).get("exp", None)
        id_dt = datetime.fromtimestamp(int(id_exp))
        at_dt = datetime.fromtimestamp(int(at_exp))
        now = datetime.now()
        later = now + self._session_refresh_interval

        # Check if tokens have expired, or expires now
        if now >= id_dt or now >= at_dt:
            _LOGGER.debug("Tokens have expired. Try to fetch new tokens")
            if await self.refresh_tokens():
                _LOGGER.debug("Successfully refreshed tokens")
            else:
                return False
        # Check if tokens expires before next update
        elif later >= id_dt or later >= at_dt:
            _LOGGER.debug("Tokens about to expire. Try to fetch new tokens")
            if await self.refresh_tokens():
                _LOGGER.debug("Successfully refreshed tokens")
            else:
                return False
        return True

    async def verify_tokens(self, token, type, client="Legacy"):
        """Verify JWT against JWK(s)."""
        if type == "identity":
            req = await self._session.get(url="https://identity.vwgroup.io/v1/jwks")
            keys = await req.json()
            audience = [
                CLIENT[client].get("CLIENT_ID"),
                "VWGMBB01DELIV1",
                "https://api.vas.eu.dp15.vwg-connect.com",
                "https://api.vas.eu.wcardp.io",
            ]
        else:
            _LOGGER.debug("Not implemented")
            return False
        try:
            pubkeys = {}
            for jwk in keys["keys"]:
                kid = jwk["kid"]
                if jwk["kty"] == "RSA":
                    pubkeys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(to_json(jwk))

            token_kid = jwt.get_unverified_header(token)["kid"]

            pubkey = pubkeys[token_kid]
            jwt.decode(token, key=pubkey, algorithms=JWT_ALGORITHMS, audience=audience)
        except Exception as error:  # pylint: disable=broad-exception-caught
            _LOGGER.debug("Failed to verify token, error: %s", error)
            return False
        return True

    async def refresh_tokens(self):
        """Refresh tokens."""
        try:
            tHeaders = {
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": USER_AGENT,
            }

            body = {
                "grant_type": "refresh_token",
                "refresh_token": self._session_tokens["identity"]["refresh_token"],
                "client_id": CLIENT["Legacy"]["CLIENT_ID"],
            }
            response = await self._session.post(
                url="https://emea.bff.cariad.digital/login/v1/idk/token",
                headers=tHeaders,
                data=body,
            )
            await self.update_service_status("token", response.status)
            if response.status == 200:
                tokens = await response.json()
                # Verify Token
                if not await self.verify_tokens(tokens["id_token"], "identity"):
                    _LOGGER.warning("Token could not be verified!")
                for token in tokens:
                    self._session_tokens["identity"][token] = tokens[token]
                self._session_headers["Authorization"] = (
                    "Bearer " + self._session_tokens["identity"]["access_token"]
                )
            else:
                _LOGGER.warning(
                    "Something went wrong when refreshing %s account tokens", BRAND
                )
                return False
        except Exception as error:  # pylint: disable=broad-exception-caught
            _LOGGER.warning("Could not refresh tokens: %s", error)
            return False
        else:
            return True

    async def update_service_status(self, url, response_code):
        """Update service status."""
        if response_code in [200, 204, 207]:
            status = "Up"
        elif response_code == 401:
            status = "Unauthorized"
        elif response_code == 403:
            status = "Forbidden"
        elif response_code == 429:
            status = "Rate limited"
        elif response_code == 1000:
            status = "Error"
        else:
            status = "Down"

        if "vehicle/v2/vehicles" in url:
            self._service_status["vehicles"] = status
        elif "parkingposition" in url:
            self._service_status["parkingposition"] = status
        elif "/vehicle/v1/trips/" in url:
            self._service_status["trips"] = status
        elif "capabilities" in url:
            self._service_status["capabilities"] = status
        elif "selectivestatus" in url:
            self._service_status["selectivestatus"] = status
        elif "token" in url:
            self._service_status["token"] = status
        else:
            _LOGGER.debug('Unhandled API URL: "%s"', url)

    async def get_service_status(self):
        """Return list of service statuses."""
        _LOGGER.debug("Getting API status updates")
        return self._service_status

    # Class helpers #
    @property
    def vehicles(self):
        """Return list of Vehicle objects."""
        return self._vehicles

    @property
    def logged_in(self):
        """Return cached logged in state.

        Not actually checking anything.
        """
        return self._session_logged_in

    def vehicle(self, vin):
        """Return vehicle object for given vin."""
        return next(
            (
                vehicle
                for vehicle in self.vehicles
                if vehicle.unique_id.lower() == vin.lower()
            ),
            None,
        )

    def hash_spin(self, challenge, spin):
        """Convert SPIN and challenge to hash."""
        spinArray = bytearray.fromhex(spin)
        byteChallenge = bytearray.fromhex(challenge)
        spinArray.extend(byteChallenge)
        return hashlib.sha512(spinArray).hexdigest()

    @property
    async def validate_login(self):
        """Check that we have a valid access token."""
        try:
            if not await self.validate_tokens:
                return False
        except OSError as error:
            _LOGGER.warning("Could not validate login: %s", error)
            return False
        else:
            return True
