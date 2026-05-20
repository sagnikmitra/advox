package com.advox.gatewayservice.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

@RestController
public class HealthCheckController {

    @GetMapping("/api/health")
    public Mono<String> health() {
        return Mono.just("Gateway service is up!");
    }
}
