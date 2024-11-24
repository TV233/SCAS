package com.kclgroup.backend.pojo.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import lombok.Data;

/**
 * 
 * @TableName top_text
 */
@TableName(value ="top_text")
@Data
public class TopText implements Serializable {
    /**
     * 
     */
    private Integer positionIndex;

    /**
     * 
     */
    private String title;

    /**
     * 
     */
    private String content;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}