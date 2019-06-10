package com.github.ssproessig.amqptraining.springbootconsumer;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.Exchange;
import org.springframework.amqp.core.ExchangeBuilder;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.core.QueueBuilder;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
public class RabbitConfiguration {

  @Value("${consumer-sample.queue-name:spring-boot-consumer}")
  private String queueName;

  @Value("${consumer-sample.binding-key:*.info}")
  private String bindingKey;

  @Bean
  public Queue queue() {
    return QueueBuilder.durable(queueName).autoDelete().build();
  }

  @Bean
  Exchange exchange() {
    return ExchangeBuilder.topicExchange("amqp-training").durable(false).build();
  }

  @Bean
  Binding binding(Queue consumerQueue, TopicExchange amqpTrainingExchange) {
    return BindingBuilder.bind(consumerQueue).to(amqpTrainingExchange).with(bindingKey);
  }
}
