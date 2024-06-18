"""
sentineltoolbox.exceptions provide all Warning and Error classes
"""

# Copyright 2024 ESA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__all__: list[str] = [
    "S3BucketCredentialNotFoundError",
    "CredentialTargetNotSupportedError",
    "SecretFileNotFoundError",
    "SecretAliasNotFoundError",
    "DataSemanticConversionError",
]


class S3BucketCredentialNotFoundError(Exception):
    """
    Cannot found S3 Bucket Credentials.
    This error give no information about validity of credentials
    """


class CredentialTargetNotSupportedError(Exception):
    """This error is raised if user tries to convert credentials to kwargs
    for a target that is not supported yet.

    To know list of supported targets, just write: :obj:`sentineltoolbox.typedefs.Credentials.available_targets`
    """


class SecretFileNotFoundError(Exception):
    pass


class SecretAliasNotFoundError(Exception):
    pass


class DataSemanticConversionError(Exception):
    """
    Semantic of a product or ADF cannot be convert "from legacy to new format" or "from new format to legacy"
    because corrspondance between legacy and new format is missing. To fix it, you need to pass new semantic
    explicitly or update legacy<->new format mapping, if available.
    """


class MultipleResultsError(Exception):
    """This error is raised if unique result is expected but matching criteria returns more than one result"""
