package com.advox.loginservice.service;

import com.advox.loginservice.dto.UserDetailsDto;
import com.advox.loginservice.entity.UserDetails;
import com.advox.loginservice.entity.UserCredentials;
import com.advox.loginservice.repository.UserCredentialsRepository;
import com.advox.loginservice.repository.UserDetailsRepository;
import com.advox.loginservice.vo.LoginVo;
import com.advox.loginservice.vo.UserRegistrationVo;
import com.advox.loginservice.vo.UserUpdateVo;
import com.advox.loginservice.dto.LoginDto;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Service for handling authentication and user management.
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class AuthService {

    private final UserCredentialsRepository credentialsRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final UserDetailsRepository userDetailsRepository;

    /**
     * Authenticates a user and issues a JWT.
     */
    public LoginDto login(LoginVo vo) {
        var user = credentialsRepository.findByEmail(vo.getEmail())
                .orElseThrow(() -> new UsernameNotFoundException("User not found for email: " + vo.getEmail()));

        if (!passwordEncoder.matches(vo.getPassword(), user.getPassword())) {
            log.warn("Invalid password attempt for email: {}", vo.getEmail());
            throw new BadCredentialsException("Invalid email or password");
        }

        // Generate token using userId as subject and email claim
        String token = jwtService.generateToken(user.getId(), user.getEmail());

        return LoginDto.builder()
                .userId(user.getId())
                .token(token)
                .build();
    }

    /**
     * Registers a new user and returns the user ID.
     */
    @Transactional
    public Long register(UserRegistrationVo vo) {
        if (credentialsRepository.findByEmail(vo.getEmail()).isPresent()) {
            throw new IllegalArgumentException("Email already exists: " + vo.getEmail());
        }

        UserCredentials credentials = UserCredentials.builder()
                .email(vo.getEmail())
                .password(passwordEncoder.encode(vo.getPassword()))
                .build();

        credentialsRepository.save(credentials);

        UserDetails details = UserDetails.builder()
                .userId(credentials.getId())
                .name(vo.getName())
                .phoneNumber(vo.getPhoneNumber())
                .barCounselId(vo.getBarCouncilId())
                .build();

        userDetailsRepository.save(details);
        System.out.println("ID: " + credentials.getId());

        return credentials.getId();
    }

    /**
     * Updates existing user details.
     */
    @Transactional
    public Long updateUserDetails(Long userId, UserUpdateVo vo) {
        var details = userDetailsRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User details not found for ID: " + userId));

        details.setName(vo.getName());
        details.setPhoneNumber(vo.getPhoneNumber());
        details.setBarCounselId(vo.getBarCouncilId());
        userDetailsRepository.save(details);

        log.info("Updated details for userId={}", userId);
        return userId;
    }

    /**
     * Retrieves user details.
     */
    public UserDetailsDto getUserDetails(Long userId) {
        var details = userDetailsRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User details not found for ID: " + userId));

        return UserDetailsDto.builder()
                .userId(details.getUserId())
                .name(details.getName())
                .phoneNumber(details.getPhoneNumber())
                .barCounselId(details.getBarCounselId())
                .build();
    }
}
