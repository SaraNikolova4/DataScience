package com.example.vvnp_f.Repository;
import com.example.vvnp_f.Models.Country;
import org.springframework.data.neo4j.repository.Neo4jRepository;
import org.springframework.data.neo4j.repository.query.Query;

import java.util.List;

public interface CountryRepository extends Neo4jRepository<Country, String> {

}
