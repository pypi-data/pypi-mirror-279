from typing import Protocol, Dict

import httpx

from kenar.errors import APIException, HTTPException


class JSONSerializable(Protocol):
    def json(self) -> str:
        ...

    def dict(self):
        ...


def _request(url: str, method: str, data: JSONSerializable, headers: Dict):
    try:
        if headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            resp = httpx.request(
                method=method,
                url=url,
                data=data.dict() if data is not None else {},
                headers=headers
            )
        else:
            resp = httpx.request(
                method=method,
                url=url,
                content=data.json() if data is not None else '',
                headers=headers
            )

        if resp.status_code == httpx.codes.OK:
            return resp
        raise APIException({"code": resp.status_code, "message": resp.text})
    except httpx.RequestError as e:
        raise HTTPException(e) from None
