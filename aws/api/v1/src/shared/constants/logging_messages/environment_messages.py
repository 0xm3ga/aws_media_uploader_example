class EnvironmentMessages:
    class Error:
        ENV_VAR_NOT_SET = "Environment variable {var_name} not set."
        MISSING_ENV_VARS = "Missing required environment variable(s): {missing_vars}"

    class Info:
        ENV_VAR_FETCHED = "Successfully fetched environment variable: {var_name}"
        ALL_ENV_VARS_FETCHED = "Successfully fetched all required environment variables."
