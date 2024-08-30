package com.example.vvnp_f.Web;

import com.example.vvnp_f.Exception.NotFoundException;
import com.example.vvnp_f.Models.PointsDTO;
import com.example.vvnp_f.Service.Points_Service;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class PredictController {

    private final Points_Service tvPointsService;

    public PredictController(Points_Service tvPointsService) {
        this.tvPointsService = tvPointsService;
    }


    @PostMapping("/givepoints")
    private String getPoints(@RequestParam String from,
                             @RequestParam String to,
                             @RequestParam String type,
                             Model model) {

        try {
            boolean isTv = "tv".equals(type);
            PointsDTO dto = tvPointsService.GivepredictedPoints(from,to, isTv);
            model.addAttribute("points", dto);
            return "points";
        } catch (NotFoundException e) {
            model.addAttribute("error", e.getMessage());
            return "prediction";
        }
    }

}
