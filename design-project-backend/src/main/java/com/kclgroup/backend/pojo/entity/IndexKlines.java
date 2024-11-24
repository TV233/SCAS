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
 * @TableName index_klines
 */
@TableName(value ="index_klines")
@Data
public class IndexKlines implements Serializable {
    /**
     * 
     */
    @TableId(type = IdType.AUTO)
    private Integer id;

    /**
     * 
     */
    private String indexCode;

    /**
     * 
     */
    private String indexName;

    /**
     * 
     */
    private String dateTime;

    /**
     * 
     */
    private BigDecimal open;

    /**
     * 
     */
    private BigDecimal close;

    /**
     * 
     */
    private BigDecimal high;

    /**
     * 
     */
    private BigDecimal low;

    /**
     * 
     */
    private Long volume;

    /**
     * 
     */
    private BigDecimal value;

    /**
     * 
     */
    private BigDecimal lastClose;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}