package com.kclgroup.backend.pojo.vo;

import lombok.Data;

import java.math.BigDecimal;

@Data
public class StockInfoVo {
    private String stockCode;
    private String stockName;
    private String industry;
    private String latestPrice;
    private String priceChangeRate;
    private String priceChange;
    private String riseSpeed;
    private Integer ratingOrgNum;
    private BigDecimal ratingBuyNum;
    private BigDecimal ratingAddNum;
    private BigDecimal ratingNeutralNum;
    private BigDecimal ratingReduceNum;
    private BigDecimal ratingSaleNum;
    private Integer year1;
    private BigDecimal eps1;
    private Integer year2;
    private BigDecimal eps2;
    private Integer year3;
    private BigDecimal eps3;
    private Integer year4;
    private BigDecimal eps4;
}
