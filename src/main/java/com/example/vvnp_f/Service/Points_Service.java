package com.example.vvnp_f.Service;

import com.example.vvnp_f.Exception.NotFoundException;
import com.example.vvnp_f.Models.PointsDTO;
import com.example.vvnp_f.Models.TV_Points;
import com.example.vvnp_f.Models.Ziri_Points;
import com.example.vvnp_f.Repository.TVPoints_Repository;
import com.example.vvnp_f.Repository.ZiriPoints_Repository;
import org.springframework.stereotype.Service;

@Service
public class Points_Service {

    private final TVPoints_Repository tvPointsRepository;
    private final ZiriPoints_Repository ziriPointsRepository;

    public Points_Service(TVPoints_Repository tvPointsRepository, ZiriPoints_Repository ziriPointsRepository) {
        this.tvPointsRepository = tvPointsRepository;
        this.ziriPointsRepository = ziriPointsRepository;
    }

    public PointsDTO GivepredictedPoints(String from, String to, Boolean isTV) throws NotFoundException
    {
        PointsDTO dto = new PointsDTO();
        if(isTV) {
            TV_Points tvPoints = tvPointsRepository.findByFromAndTo(from.toLowerCase(), to.toLowerCase());
            if(tvPoints == null)
            {
               throw new NotFoundException("TV predicted points from " + from + " to " + to + " not found");
            }
            dto.setTo(tvPoints.getTo());
            dto.setFrom(tvPoints.getFrom());
            dto.setPredictedPoints(tvPoints.getPredictedPoints());
            return dto;
        }
        if(!isTV) {
            Ziri_Points ziriPoints = ziriPointsRepository.findByFromAndTo(from.toLowerCase(), to.toLowerCase());
            if (ziriPoints == null) {
                throw new NotFoundException("Ziri predicted points from " + from + "to " + to + " not found!");
            }
            dto.setTo(ziriPoints.getTo());
            dto.setFrom(ziriPoints.getFrom());
            dto.setPredictedPoints(ziriPoints.getPredictedPoints());
            return dto;
        }
        return null;
    }
}
