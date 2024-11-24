package com.kclgroup.backend.pojo.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import lombok.Data;

/**
 * 
 * @TableName sectors_and_stocks
 */
@TableName(value ="sectors_and_stocks")
@Data
public class SectorsAndStocks implements Serializable {
    /**
     * 
     */
    private String sector;

    /**
     * 
     */
    private String reason;

    /**
     * 
     */
    private String stockCode;

    /**
     * 
     */
    private String stockName;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}