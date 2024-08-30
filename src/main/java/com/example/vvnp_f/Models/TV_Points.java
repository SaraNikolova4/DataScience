package com.example.vvnp_f.Models;


import jakarta.persistence.*;
import lombok.Data;
import lombok.NonNull;


@Entity
@Data
@Table(name = "table1")
public class TV_Points {

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
