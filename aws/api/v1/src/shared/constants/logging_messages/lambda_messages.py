class LambdaMessages:
    class Error:
        ERROR_INVOKING_LAMBDA = "Error occurred while invoking Lambda function: {}"
        ERROR_PROCESSING_RESPONSE = "Error occurred while processing Lambda function response: {}"
        ERROR_DURING_PROCESSING = "Error occurred during processing: {error}"
        ERROR_UNSUPPORTED_FILE_TYPE = "File type {} not supported. Cannot process."

    class Info:
        LAMBDA_INVOKED = "Lambda invoked: {request_id}. Event: {event}"
        LAMBDA_COMPLETED = "Lambda execution completed: {request_id}"
