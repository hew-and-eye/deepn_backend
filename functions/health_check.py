def handler(event, context):
  print('Hello health check')
  return { "status": "healthy" }
