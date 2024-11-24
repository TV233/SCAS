package com.kclgroup.backend.pojo.vo;

import lombok.Data;

import java.math.BigDecimal;

@Data
public class IndexKlineVo {
    private String indexCode;

    private String indexName;

    private String dateTime;
    private BigDecimal open;


    private BigDecimal close;

    private BigDecimal high;

    private BigDecimal low;

    private Long volume;

    private BigDecimal value;

    private BigDecimal lastClose;
}
