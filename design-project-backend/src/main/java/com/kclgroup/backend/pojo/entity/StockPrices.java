package com.kclgroup.backend.pojo.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import java.math.BigDecimal;
import lombok.Data;

/**
 * 
 * @TableName stock_prices
 */
@TableName(value ="stock_prices")
@Data
public class StockPrices implements Serializable {
    /**
     * 
     */
    @TableId(type = IdType.AUTO)
    private Integer id;

    /**
     * 
     */
    private String stockCode;

    /**
     * 
     */
    private BigDecimal latestPrice;

    /**
     * 
     */
    private BigDecimal priceChangeRate;

    /**
     * 
     */
    private BigDecimal priceChange;

    /**
     * 
     */
    private BigDecimal riseSpeed;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}