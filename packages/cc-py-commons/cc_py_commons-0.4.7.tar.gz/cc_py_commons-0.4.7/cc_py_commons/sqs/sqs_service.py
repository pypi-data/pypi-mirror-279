import boto3

class SqsService:
	def send(self, queue_url, message, delaySeconds=0, messageGroupId=None):
		'''
		Sends a message to the specified queue and returns the messageId. 
		The messageId can be used to lookup and delete the message in the queue.
		'''
		sqs = boto3.client('sqs')
		response = sqs.send_message(
			QueueUrl=queue_url,
			MessageBody=message,
			DelaySeconds=delaySeconds,
			MessageAttributes={},
			MessageGroupId=messageGroupId
		)
		return response.get('MessageId')
