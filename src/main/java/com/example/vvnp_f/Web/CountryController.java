package com.example.vvnp_f.Web;

import com.example.vvnp_f.Models.ConnectedDTO;
import com.example.vvnp_f.Models.ConnectedTo;
import com.example.vvnp_f.Models.Country;
import com.example.vvnp_f.Service.CountryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.Banner;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@Controller
public class CountryController {

    private final CountryService countryService;
    public CountryController(CountryService countryService) {
        this.countryService = countryService;
    }

    @GetMapping("/countries")
    public String getAllCountries(Model model) {
        List<Country> countries = countryService.getAllCountries();
        model.addAttribute("countries", countries);
        return "countries";
    }

    @GetMapping("/prediction")
    public String showPredictionPage() {
        return "prediction";
    }

    @GetMapping("/pointsReceived")
    public String getPointsReceived(@RequestParam String countryName, Model model) {
        // Логика за добивање на поени кој ги добила земјата
        List<ConnectedTo> connected = countryService.dobieni(countryName);
        model.addAttribute("connected", connected);
        return "pointsReceived";
    }

    @GetMapping("/pointsGiven")
    public String getPointsGiven(@RequestParam String countryName, Model model) {
        // Логика за добивање на поени кој ги дала земјата
        List<ConnectedTo> connected = countryService.dadeni(countryName);
        model.addAttribute("connected", connected);
        return "pointsGiven";
    }

    @GetMapping("/history")
    public String showHistory(@RequestParam("start") String startNode,
                              @RequestParam("end") String endNode,
                              Model model) {

        List<ConnectedDTO> logicdadeni = countryService.logicdadeni(startNode, endNode);
        model.addAttribute("ConnectDTO", logicdadeni);
        model.addAttribute("startNode", startNode);
        model.addAttribute("endNode", endNode);
        System.out.println(logicdadeni);
        return "history";
    }

    @GetMapping("/home")
    public String home()
    {
        return "home";
    }
}
