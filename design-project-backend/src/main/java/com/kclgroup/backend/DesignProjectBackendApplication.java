package com.kclgroup.backend;

import lombok.extern.log4j.Log4j;
import org.apache.ibatis.annotations.Mapper;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.kclgroup.backend.mapper")
public class DesignProjectBackendApplication {

	public static void main(String[] args) {
		SpringApplication.run(DesignProjectBackendApplication.class, args);
	}

}
