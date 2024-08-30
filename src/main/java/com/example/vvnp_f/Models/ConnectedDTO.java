package com.example.vvnp_f.Models;

import lombok.Data;
import org.springframework.stereotype.Component;

@Data
@Component
public class ConnectedDTO {

    private String points;
    private String year;
    private String type;
}
