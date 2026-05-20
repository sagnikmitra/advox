package com.advox.loginservice.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
public class UserRegistrationVo {

    @Schema(description = "Email ID for the new user", example = "newuser@advox.in")
    private String email;

    @Schema(description = "User's raw password", example = "password123")
    private String password;

    @Schema(description = "Full name of the user", example = "John Doe")
    private String name;

    @Schema(description = "Phone number of the user", example = "9876543210")
    private String phoneNumber;

    @Schema(description = "Bar Council ID", example = "BAR123456")
    private String barCouncilId;
}
