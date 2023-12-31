class RdsMessages:
    class Error:
        GENERIC_ERROR = "Unexpected error occurred"
        RDS_COMMUNICATION_ERROR = "Error communicating with RDS: {error}"
        MISSING_VARIABLES_IN_RESPONSE = "Invalid RDS response, missing required variables: {error}"
        UNEXPECTED_ERROR = "Unexpected error occurred: {error}"

    class Info:
        FETCH_RDS_DATA_SUCCESS = "Successfully fetched data from RDS for filename: {filename}"
        FETCH_MEDIA_INFO_SUCCESS = (
            "Successfully fetched media information from RDS for filename: {filename}"
        )
