package com.kclgroup.backend.pojo.vo;

import lombok.Data;
import java.math.BigDecimal;
import java.util.Date;

@Data
public class PredictionVo {
    private String modelName;
    private Date predictionDate;
    private BigDecimal predictedPrice;
    private BigDecimal accuracy;
    private BigDecimal confidenceLevel;
    private String predictionBasis;
} 