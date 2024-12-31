package com.kclgroup.backend.pojo.vo;

import lombok.Data;
import java.math.BigDecimal;

@Data
public class PredictionSummaryVo {
    private String mostAccurateModel;
    private BigDecimal oneWeekChange;
    private BigDecimal oneMonthChange;
    private BigDecimal threeMonthChange;
    private BigDecimal modelAccuracy;
} 