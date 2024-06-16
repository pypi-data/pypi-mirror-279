from __future__ import annotations

import json
import logging

import chardet
import httpx

log = logging.getLogger("red_utils.ext.httpx_utils.decoders.response_decoders")


def autodetect_charset(content: bytes = None):
    """Attempt to automatically detect encoding from input bytestring."""
    try:
        ## Detect encoding from bytes
        _encoding: str | None = chardet.detect(byte_str=content).get("encoding")

        if not _encoding:
            ## Default to utf-8
            _encoding = "utf-8"

        return _encoding

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception auto-detecting character set for input bytestring. Details: {exc}"
        )
        log.error(msg)
        log.warning("Defaulting to utf-8")

        return "utf-8"


def decode_res_content(self, res: httpx.Response = None) -> dict:
    """Use multiple methods to attempt to decode an `httpx.Response.content` bytestring.

    Params:
        res (httpx.Response): An `httpx.Response` object, with `.content` to be decoded.

    Returns:
        (dict): A `dict` from the `httpx.Response`'s `.content` param.

    """
    assert res, ValueError("Missing httpx Response object")
    assert isinstance(res, httpx.Response), TypeError(
        f"res must be of type httpx.Response. Got type: ({type(res)})"
    )

    _content: bytes = res.content
    assert _content, ValueError("Response content is empty")
    assert isinstance(_content, bytes), TypeError(
        f"Expected response.content to be a bytestring. Got type: ({type(_content)})"
    )

    ## Get content's encoding, or default to 'utf-8'
    try:
        decode_charset: str = autodetect_charset(content=_content)
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception detecting response content's encoding. Details: {exc}"
        )
        log.error(msg)
        log.trace(exc)
        log.warning(f"Defaulting to 'utf-8'")

        decode_charset: str = "utf-8"

    ## Decode content
    try:
        _decode: str = res.content.decode(decode_charset)

    except Exception as exc:
        ## Decoding failed, retry with different encodings
        msg = Exception(
            f"[Attempt 1/2] Unhandled exception decoding response content. Details: {exc}"
        )
        log.warning(msg)

        if not res.encoding == "utf-8":
            ## Try decoding again, using response's .encoding param
            log.warning(
                f"Retrying response content decode with encoding '{res.encoding}'"
            )
            try:
                _decode = res.content.decode(res.encoding)
            except Exception as exc:
                inner_msg = Exception(
                    f"[Attempt 2/2] Unhandled exception decoding response content. Details: {exc}"
                )
                log.error(inner_msg)

                raise inner_msg

        else:
            ## Decoding with utf-8 failed, attempt with ISO-8859-1
            #  https://en.wikipedia.org/wiki/ISO/IEC_8859-1
            log.warning(
                f"Detected UTF-8 encoding, but decoding as UTF-8 failed. Retrying with encoding ISO-8859-1."
            )
            try:
                _decode = res.content.decode("ISO-8859-1")
            except Exception as exc:
                msg = Exception(
                    f"Failure attempting to decode content as UTF-8 and ISO-8859-1. Details: {exc}"
                )

                raise msg

    ## Load decoded content into dict
    try:
        _json: dict = json.loads(_decode)

        return _json

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception loading decoded response content to dict. Details: {exc}"
        )

        raise msg
