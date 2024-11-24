package com.kclgroup.backend.pojo.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import lombok.Data;

/**
 * 
 * @TableName market_style
 */
@TableName(value ="market_style")
@Data
public class MarketStyle implements Serializable {
    /**
     * 
     */
    private String name;

    /**
     * 
     */
    private Double changeRate;

    /**
     * 
     */
    private String topName;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}