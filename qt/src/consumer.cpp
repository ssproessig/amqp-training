#include <QCoreApplication>

#include "qamqp/qamqpclient.h"
#include "qamqp/qamqpexchange.h"
#include "qamqp/qamqpqueue.h"



namespace
{
    namespace AmqpConstants
    {
        QString const uri = "amqp://guest:guest@localhost:5672/";

        QString const exchangeName = "amqp-training";

        QString const queueName = "qt-consumer";

        QString const bindingKey = "*.info";
    }


    class Consumer final : public QObject
    {
    public:
        explicit Consumer(QString const& aBindingKey, QString const& aQueueName): QObject(nullptr)
        {
            client.setAutoReconnect(true);

            connect(&client, &QAmqpClient::connected, this, [ = ]()
            {
                qDebug() << "[i] Declaring queue " << aQueueName << " as auto-delete";

                auto const queue = client.createQueue(aQueueName);
                queue->declare(QAmqpQueue::AutoDelete);
                connect(queue, &QAmqpQueue::declared, this, [ = ]()
                {
                    connect(queue, &QAmqpQueue::messageReceived, this, [ = ]()
                    {
                        auto const message = queue->dequeue();
                        qDebug() << "     " << message.routingKey() << ":  " << message.payload();
                    });

                    qDebug() << "[i] Waiting for messages. To exit press CTRL+C";
                    queue->consume(QAmqpQueue::NoOptions);
                });



                qDebug() << "[i] Declaring exchange " << AmqpConstants::exchangeName << " as topic";
                auto const exchange = client.createExchange(AmqpConstants::exchangeName);
                exchange->declare(QAmqpExchange::Topic, QAmqpExchange::NoOptions);



                qDebug() << "[i] Binding exchange " << AmqpConstants::exchangeName
                         << " to queue " << aQueueName
                         << " with " << aBindingKey;
                queue->bind(AmqpConstants::exchangeName, aBindingKey);
            });
        }

        void connectToAndUse()
        {
            qDebug() << "[i] Connecting to " << AmqpConstants::uri;
            client.connectToHost(AmqpConstants::uri);
        }

    private:
        QAmqpClient client;
    };

}



int main(int argc, char** argv)
{
    QCoreApplication app(argc, argv);
    const auto& args = QCoreApplication::arguments();

    auto const argLen = args.size();

    Consumer c(
        argLen > 1 ? args.at(1) : AmqpConstants::bindingKey,
        argLen > 2 ? args.at(2) : AmqpConstants::queueName
    );
    c.connectToAndUse();

    return QCoreApplication::exec();
}
