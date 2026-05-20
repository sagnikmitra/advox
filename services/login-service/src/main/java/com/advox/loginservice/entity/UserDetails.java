package com.advox.loginservice.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "user_details")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserDetails {
    @Id
    private Long userId;  // same as user_credentials.id

    @Column(nullable = false)
    private String name;

    @Column
    private String phoneNumber;

    @Column(unique = true)
    private String barCounselId;
}
