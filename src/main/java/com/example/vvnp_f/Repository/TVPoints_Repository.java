package com.example.vvnp_f.Repository;

import com.example.vvnp_f.Models.TV_Points;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TVPoints_Repository extends JpaRepository<TV_Points, Long> {

   TV_Points findByFromAndTo(String from, String to);
}
