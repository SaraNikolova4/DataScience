package com.example.vvnp_f.Service;
import com.example.vvnp_f.Models.ConnectedDTO;
import com.example.vvnp_f.Models.ConnectedTo;
import com.example.vvnp_f.Models.Country;
import com.example.vvnp_f.Repository.ConnectedToRepository;
import com.example.vvnp_f.Repository.CountryRepository;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
@Transactional
public class CountryService {

    @Autowired
    private CountryRepository countryRepository;
    @Autowired
    private ConnectedToRepository connectedToRepository;

    public Country getCountryByName(String name) {
        return countryRepository.findById(name).orElse(null);
    }

    public void saveCountry(Country country) {
        countryRepository.save(country);
    }

    public List<Country> getAllCountries() {
        return countryRepository.findAll();
    }


    @Transactional
    public void saveCountryFromStringData(String name, String finals, String semi1, String semi2, int semiCount1, int semiCount2, int finalsCount) {
        Country country = new Country();
        country.setName(name);
        country.setFinals(finals != null ? finals : "[]");
        country.setSemi1(semi1 != null ? semi1 : "[]");
        country.setSemi2(semi2 != null ? semi2 : "[]");
        country.setSemiCount1(semiCount1);
        country.setSemiCount2(semiCount2);
        country.setFinalsCount(finalsCount);

        // Save country
        countryRepository.save(country);
    }

    public List<ConnectedTo> dadeni(String name) {
        List<ConnectedTo> connects = new ArrayList<>();
        for (ConnectedTo connected : connectedToRepository.findAllConnections()) {
            if (connected.getStartNode().equals(name)) {
                connects.add(connected);
            }
        }
        System.out.println(connects);
        return connects;
    }

    public List<ConnectedTo> dobieni(String countryName) {

        List<ConnectedTo> connects = new ArrayList<>();
        for (ConnectedTo connected : connectedToRepository.findAllConnections()) {
            if (connected.getEndNode().equals(countryName)) {
                connects.add(connected);
            }
        }
        System.out.println(connects);
        return connects;
    }

    public List<ConnectedDTO> logicdadeni(String startNode, String endNode) {

        List<ConnectedTo> connected = connectedToRepository.findAllConnections();
        List<ConnectedDTO> connectedDTOS = new ArrayList<>();
        for (ConnectedTo connectedTo : connected) {
            if (connectedTo.getStartNode().equals(startNode) && connectedTo.getEndNode().equals(endNode)) {
                List<Integer> points = connectedTo.getPoints();
                List<Integer> years = connectedTo.getYears();
                List<Integer> pointsTypes = connectedTo.getPointsTypes();
                int maxSize = Math.max(points.size(), Math.max(years.size(), pointsTypes.size()));

                for (int i = 0; i < maxSize; i++) {
                    ConnectedDTO connectedDTO = new ConnectedDTO();

                    if (i < points.size()) {
                        connectedDTO.setPoints(points.get(i).toString());
                    }

                    if (i < years.size()) {
                        connectedDTO.setYear(years.get(i).toString());
                    }

                    if (i < pointsTypes.size()) {
                        if (pointsTypes.get(i) == 1) {
                            String s = "Televolters";
                        }
                        String s = "Ziri";
                        connectedDTO.setType(s);
                    }

                    connectedDTOS.add(connectedDTO);
                }
            }
        }
        return connectedDTOS;
    }
}

