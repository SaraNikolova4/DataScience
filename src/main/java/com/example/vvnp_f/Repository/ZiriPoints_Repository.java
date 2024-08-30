package com.example.vvnp_f.Repository;

import com.example.vvnp_f.Models.TV_Points;
import com.example.vvnp_f.Models.Ziri_Points;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface ZiriPoints_Repository extends JpaRepository<Ziri_Points, Long> {

    Ziri_Points findByFromAndTo(String from, String to);
}
