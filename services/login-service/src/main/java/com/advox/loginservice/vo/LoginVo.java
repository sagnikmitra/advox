package com.advox.loginservice.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
public class LoginVo {

    @Schema(description = "Email ID of the user", example = "admin@advox.in")
    private String email;

    @Schema(description = "User's password", example = "advox123")
    private String password;
}
