package com.kclgroup.backend.pojo.entity;

import lombok.Data;
import java.math.BigDecimal;
import java.util.Date;

@Data
public class Prediction {
    private Integer id;
    private String stockCode;
    private String modelName;
    private Date predictionDate;
    private BigDecimal predictedPrice;
    private Date createdAt;
    private BigDecimal accuracy;
    private String predictionBasis;
    private BigDecimal sentimentScore;
    private BigDecimal confidenceLevel;
} 