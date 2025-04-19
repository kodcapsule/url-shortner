

## DynamoDB Table Attributes
TableName : url-shortener
urlId: String ()
originalUrl: String
shortUrl: String
createdAt: String (ISO format)
description: String
clicks: Number


# REf
1. https://kinsta.com/blog/url-shortener-with-python/
2. https://docs.aws.amazon.com/lambda/latest/dg/python-layers.html


# CHALLEMGES ERRORS
1. [ERROR] Runtime.ImportModuleError: Unable to import module 'lambda_function': No module named 'pyshorteners'
description: {
  "errorMessage": "Unable to import module 'lambda_function': No module named 'pyshorteners'",
  "errorType": "Runtime.ImportModuleError",
  "requestId": "",
  "stackTrace": []
}
- Solution: Use