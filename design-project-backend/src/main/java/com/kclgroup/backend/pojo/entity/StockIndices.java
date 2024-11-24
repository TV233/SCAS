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
 * @TableName stock_indices
 */
@TableName(value ="stock_indices")
@Data
public class StockIndices implements Serializable {
    /**
     * 
     */
    @TableId(type = IdType.AUTO)
    private Integer id;

    /**
     * 
     */
    private String symbol;

    /**
     * 
     */
    private String name;

    /**
     * 
     */
    private BigDecimal indexValue;

    /**
     * 
     */
    private BigDecimal changePercent;

    /**
     * 
     */
    private BigDecimal changeAmount;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}