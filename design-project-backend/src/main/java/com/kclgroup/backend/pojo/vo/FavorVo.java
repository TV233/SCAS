package com.kclgroup.backend.pojo.vo;

import lombok.Data;

import java.util.Date;

@Data
public class FavorVo {
    private String stockName;
    private String stockCode;
    private float latestPrice;
    private float priceChange;
    private float priceChangeRate;
}
