package com.kclgroup.backend.pojo.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import lombok.Data;

/**
 * 
 * @TableName stock_info
 */
@TableName(value ="stock_info")
@Data
public class StockInfo implements Serializable {
    /**
     * 
     */
    @TableId
    private String stockCode;

    /**
     * 
     */
    private String stockName;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}