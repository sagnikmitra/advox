package com.advox.loginservice.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Builder;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@Data
@Getter
@Setter
@Builder
public class LoginDto {

    @Schema(description = "User Id", example = "1")
    private Long userId;

    @Schema(description = "JWT token for authenticated user")
    private String token;
}
