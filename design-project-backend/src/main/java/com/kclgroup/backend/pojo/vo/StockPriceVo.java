package com.kclgroup.backend.pojo.vo;

import lombok.Data;

@Data
public class StockPriceVo {
    private String stockCode;
    private String stockName;
    private String latestPrice;
    private String priceChangeRate;
    private String priceChange;
    private String riseSpeed;
}
