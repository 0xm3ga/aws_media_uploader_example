class LambdaMessages:
    class Error:
        GENERIC_ERROR = "Generic Lambda error occured."
        ERROR_INVOKING_LAMBDA = "Error occurred while invoking Lambda function: {error}"
        ERROR_PROCESSING_RESPONSE = (
            "Error occurred while processing Lambda function response: {error}"
        )

        # TODO: review
        ERROR_DURING_PROCESSING = "Error occurred during processing: {error}"

    class Info:
        LAMBDA_INVOKED = "Lambda invoked: {request_id}. Event: {event}"
        LAMBDA_COMPLETED = "Lambda execution completed: {request_id}"
