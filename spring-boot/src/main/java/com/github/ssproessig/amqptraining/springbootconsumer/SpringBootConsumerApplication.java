package com.github.ssproessig.amqptraining.springbootconsumer;

import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.Exchange;
import org.springframework.amqp.rabbit.annotation.Queue;
import org.springframework.amqp.rabbit.annotation.QueueBinding;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


@SpringBootApplication
@Slf4j
public class SpringBootConsumerApplication {

  public static void main(String[] args) {
    SpringApplication.run(SpringBootConsumerApplication.class, args);
  }


  @RabbitListener(
      bindings = @QueueBinding(
          value = @Queue(
              name = "spring-boot-consumer"
          ),
          exchange = @Exchange(
              name = "amqp-training",
              type = "topic",
              durable = "false"
          ),
          key = "*.info"
      )
  )
  public void onMessage(Message aMessage) {
    String payload = new String(aMessage.getBody());

    log.info("{} - {}",
        StringUtils.leftPad(
            aMessage.getMessageProperties().getReceivedRoutingKey(), 20),
        payload);
  }
}
