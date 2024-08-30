package com.example.vvnp_f;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.neo4j.repository.config.EnableNeo4jRepositories;

@SpringBootApplication
@EnableNeo4jRepositories(basePackages = "com.example.vvnp_f.Repository")
public class VvnpFApplication {

	public static void main(String[] args) {
		SpringApplication.run(VvnpFApplication.class, args);
	}

}
