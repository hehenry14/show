import pika
import os
import json
import logging
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .models import User, Product, UserInfo, ProductInfo

local_models = ['User', 'Product']


class Show:

    def __init__(self):
        # set up the RMQ
        rmq_config = self.__get_configs_rmq()
        credentials = pika.PlainCredentials(rmq_config['user'], rmq_config['pass'])
        parameters = pika.ConnectionParameters(host=rmq_config['host'], port=rmq_config['port'], credentials=credentials)
        self._connection = pika.BlockingConnection(parameters)
        self._logger = logging.getLogger(__name__)

        # set up the Postgres
        postgre_config = self.__get_cofig_postgres()
        postgres_location = f"postgresql://{postgre_config['user']}:{postgre_config['pass']}@{postgre_config['host']}/"
        self._engine = create_engine(postgres_location)


    @staticmethod
    def __get_configs_rmq() -> dict:
        return {
            'host': os.getenv('RMQ_HOST'),
            'port': os.getenv('RMQ_PORT'),
            # 'virtual_host': os.getenv('RMQ_VIRTUALHOST'),
            'user': os.getenv('RMQ_USER'),
            'pass': os.getenv('RMQ_PASS')
        }

    @staticmethod
    def __get_cofig_postgres() -> dict:
        return {
            'host': os.getenv('POSTGRES_HOST'),
            'user': os.getenv('POSTGRES_USER'),
            'pass': os.getenv('POSTGRES_PASS'),
        }

    def execute(self):
        channel = self._connection.channel()
        channel.basic_consume(queue='in_stock', on_message_callback=self.callback)
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()

    def callback(self, ch, method, properties, body):
        # message looks like this '{"product_id": 1, "user_id": 1}' Then we will get the credentials and product site
        # information from the Postgres db and do the purchase.
        message = json.loads(body)

        with Session(self._engine) as session:
            user_config_row = session.query(User.config).filter(User.id == message['user_id']).one_or_none()
            product_config_row = session.query(Product.config).filter(Product.id == message['product_id']).one_or_none()

        if user_config_row is None or product_config_row is None:
            self._logger.error(f"User_id: {message['user_id']} or product_id: {message['product_id']} does not exist.")
            return

        self.purchase(user_config_row[0], product_config_row[0])

    def purchase(self, user_config: dict, product_config: dict):
        """
        This function will automatically purchase the item specified in the input message
        :return:
        """
        user_info = UserInfo(user_config)
        product_info = ProductInfo(product_config)

    def log_in(self, credentials: dict, product_info: ProductInfo):
        """
        This function logs user in.
        :param credentials: the log in credentials from the user.
        :param product_info: the ProductInfo with the given product id.
        :return:
        """
        r = product_info.get_login_request(credentials)
        ...