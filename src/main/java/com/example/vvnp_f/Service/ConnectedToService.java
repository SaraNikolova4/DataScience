package com.example.vvnp_f.Service;
import com.example.vvnp_f.Models.ConnectedTo;
import com.example.vvnp_f.Repository.ConnectedToRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class ConnectedToService {


    public ConnectedToService(ConnectedToRepository connectedToRepository) {
        this.connectedToRepository = connectedToRepository;
    }

    private final ConnectedToRepository connectedToRepository;

    public List<ConnectedTo> getAllConnections() {
        return connectedToRepository.findAllConnections();
    }

}
