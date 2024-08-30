package com.example.vvnp_f.Models;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Data
@Table(name = "table2")
public class Ziri_Points {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "`From`")
    private String from;

    @Column(name = "`To`")
    private String to;

    @Column(name = "Predicted_Points")
    private int predictedPoints;

}