package com.kclgroup.backend.pojo.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.io.Serializable;
import lombok.Data;

/**
 * 
 * @TableName emotion_index
 */
@TableName(value ="emotion_index")
@Data
public class EmotionIndex implements Serializable {
    /**
     * 
     */
    private Double emotionIndex;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}