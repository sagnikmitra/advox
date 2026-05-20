package com.advox.loginservice.service;

import com.advox.loginservice.config.JwtProperties;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.security.Key;
import java.util.Date;

/**
 * Service for generating and parsing JWT tokens using configured properties.
 */
@Service
public class JwtService {

    private final JwtProperties jwtProperties;
    private Key signingKey;

    public JwtService(JwtProperties jwtProperties) {
        this.jwtProperties = jwtProperties;
    }

    @PostConstruct
    public void init() {
        byte[] secretBytes = jwtProperties.getSecret().getBytes(StandardCharsets.UTF_8);
        this.signingKey = Keys.hmacShaKeyFor(secretBytes);
    }

    /**
     * Generate a JWT token using userId as subject and email as a custom claim.
     */
    public String generateToken(Long userId, String email) {
        long nowMillis = System.currentTimeMillis();
        Date now = new Date(nowMillis);
        Date expiry = new Date(nowMillis + jwtProperties.getExpirationMillis());

        return Jwts.builder()
                .setSubject(String.valueOf(userId))
                .claim("email", email)
                .setIssuedAt(now)
                .setExpiration(expiry)
                .signWith(signingKey, SignatureAlgorithm.forName(jwtProperties.getAlgorithm()))
                .compact();
    }

    /**
     * Extract the user ID (subject) from the token.
     */
    public Long extractUserId(String token) {
        Claims claims = parseToken(token);
        return Long.parseLong(claims.getSubject());
    }

    /**
     * Parse and validate the JWT, returning its claims.
     */
    public Claims parseToken(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(signingKey)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    /**
     * Check if a token has expired.
     */
    public boolean isTokenExpired(String token) {
        Date expiration = parseToken(token).getExpiration();
        return expiration.before(new Date());
    }

    /**
     * Validate token by userId.
     */
    public boolean validateToken(String token, Long expectedUserId) {
        try {
            Long userId = extractUserId(token);
            return userId.equals(expectedUserId) && !isTokenExpired(token);
        } catch (Exception e) {
            return false;
        }
    }
}
