package com.advox.loginservice.controller;

import com.advox.loginservice.dto.ApiResponse;
import com.advox.loginservice.dto.UserDetailsDto;
import com.advox.loginservice.dto.LoginDto;
import com.advox.loginservice.service.AuthService;
import com.advox.loginservice.service.JwtService;
import com.advox.loginservice.vo.LoginVo;
import com.advox.loginservice.vo.UserRegistrationVo;
import com.advox.loginservice.vo.UserUpdateVo;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.Instant;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;
    private final JwtService jwtService;

    @PostMapping("/login")
    public ResponseEntity<ApiResponse<LoginDto>> login(@RequestBody LoginVo vo) {
        LoginDto dto = authService.login(vo);
        ApiResponse<LoginDto> response = new ApiResponse<>(
                true,
                "Login successful",
                dto,
                Instant.now()
        );
        return ResponseEntity.ok(response);
    }

    @PostMapping("/register")
    public ResponseEntity<ApiResponse<Long>> register(@RequestBody UserRegistrationVo vo) {
        Long userId = authService.register(vo);
        ApiResponse<Long> response = new ApiResponse<>(
                true,
                "User created successfully!",
                userId,
                Instant.now()
        );
        return ResponseEntity.ok(response);
    }

    @PutMapping("/me")
    public ResponseEntity<ApiResponse<Long>> updateMyDetails(@RequestHeader("X-USER-ID") Long userId, @RequestBody UserUpdateVo updateVo) {
        Long updatedUserId = authService.updateUserDetails(userId, updateVo);

        ApiResponse<Long> response = new ApiResponse<>(
                true,
                "User details updated successfully",
                updatedUserId,
                Instant.now()
        );
        return ResponseEntity.ok(response);
    }

    @GetMapping("/me")
    public ResponseEntity<ApiResponse<UserDetailsDto>> getMyDetails(@RequestHeader("X-USER-ID") Long userId) {
        UserDetailsDto userDetails = authService.getUserDetails(userId);

        ApiResponse<UserDetailsDto> response = new ApiResponse<>(
                true,
                "User details fetched successfully",
                userDetails,
                Instant.now()
        );
        return ResponseEntity.ok(response);
    }
}
