package com.advox.loginservice.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class UserDetailsDto {
    private Long userId;
    private String name;
    private String phoneNumber;
    private String barCounselId;
}
