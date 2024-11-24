package com.kclgroup.backend.mapper;

import com.kclgroup.backend.pojo.entity.MarketStyle;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

/**
* @author 张小明
* @description 针对表【market_style】的数据库操作Mapper
* @createDate 2024-06-24 21:07:10
* @Entity com.kclgroup.backend.pojo.entity.MarketStyle
*/
@Mapper
public interface MarketStyleMapper extends BaseMapper<MarketStyle> {

    @Select("SELECT * FROM market_style")
    List<MarketStyle> getMarketStyle();
}




