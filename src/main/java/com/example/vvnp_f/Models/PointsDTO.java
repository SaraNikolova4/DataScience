package com.example.vvnp_f.Models;

import lombok.Data;
import org.springframework.stereotype.Component;


@Component
@Data
public class PointsDTO {

    private String from;

    private String to;

    private int predictedPoints;
}
