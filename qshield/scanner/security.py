import os
import re
import zipfile
from typing import Tuple
from urllib.parse import urlparse

def validate_zip_archive(zip_file_obj, target_dir: str = "/tmp") -> Tuple[bool, str]:
    """
    Validates a zip archive to ensure no file entry escapes target_dir (ZIP-slip protection).
    """
    try:
        with zipfile.ZipFile(zip_file_obj, "r") as zf:
            target_abs = os.path.abspath(target_dir)
            for member in zf.infolist():
                # Check for absolute paths or path traversal prefixes
                member_path = member.filename
                if member_path.startswith("/") or member_path.startswith("\\"):
                    return False, f"ZIP-slip detected: absolute path '{member_path}'"
                
                # Resolve full destination path
                dest_path = os.path.abspath(os.path.join(target_abs, member_path))
                if not (dest_path == target_abs or dest_path.startswith(target_abs + os.sep)):
                    return False, f"ZIP-slip detected: directory traversal in '{member_path}'"
        return True, "Archive verified safe"
    except Exception as e:
        return False, f"Invalid zip archive: {str(e)}"

def sanitize_git_url(url: str) -> Tuple[bool, str]:
    """
    Validates a Git repository URL against malicious command injection and non-HTTPS protocols.
    """
    if not url or not isinstance(url, str):
        return False, "Empty or non-string URL"
    
    url = url.strip()
    
    # Check for shell metacharacters / injection attempts
    dangerous_chars = [";", "|", "&", "$", "`", "\n", "\r", "<", ">", "\x00"]
    if any(char in url for char in dangerous_chars):
        return False, "Unsafe characters detected in repository URL"
    
    parsed = urlparse(url)
    if parsed.scheme.lower() not in ["https", "http"]:
        return False, f"Disallowed URL scheme '{parsed.scheme}'. Only https:// or http:// allowed"
    
    if not parsed.netloc:
        return False, "Invalid URL: missing network location/host"
        
    return True, url
