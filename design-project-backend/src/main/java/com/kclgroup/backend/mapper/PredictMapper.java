package com.kclgroup.backend.mapper;

import com.kclgroup.backend.pojo.entity.Predict;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.kclgroup.backend.pojo.vo.PredictVo;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.math.BigDecimal;
import java.util.List;

/**
* @author 张小明
* @description 针对表【predict】的数据库操作Mapper
* @createDate 2024-06-24 21:18:07
* @Entity com.kclgroup.backend.pojo.entity.Predict
*/
@Mapper
public interface PredictMapper extends BaseMapper<Predict> {
    @Select("SELECT p.stock_code,s.stock_name FROM predict p,stock_info s where p.stock_code = s.stock_code order by RATING_ORG_NUM DESC limit 20")
    List<PredictVo> getPredict();
    @Select("SELECT RATING_ORG_NUM FROM predict WHERE STOCK_CODE = #{stockCode}")
    Integer getRatingOrgNum(String stockCode);
    @Select("SELECT RATING_BUY_NUM FROM predict WHERE STOCK_CODE = #{stockCode}")
    BigDecimal getRatingBuyNum(String stockCode);
    @Select("SELECT RATING_ADD_NUM FROM predict WHERE STOCK_CODE = #{stockCode}")
    BigDecimal getRatingAddNum(String stockCode);
    @Select("SELECT RATING_SALE_NUM FROM predict WHERE STOCK_CODE = #{stockCode}")
    BigDecimal getRatingSaleNum(String stockCode);
    @Select("SELECT RATING_NEUTRAL_NUM FROM predict WHERE STOCK_CODE = #{stockCode}")
    BigDecimal getRatingNeutralNum(String stockCode);
    @Select("SELECT RATING_REDUCE_NUM FROM predict WHERE STOCK_CODE = #{stockCode}")
    BigDecimal getRatingReduceNum(String stockCode);
    @Select("SELECT YEAR1 FROM predict WHERE STOCK_CODE = #{stockCode}")
    Integer getYear1(String stockCode);
    @Select("SELECT EPS1 FROM predict WHERE STOCK_CODE = #{stockCode}")
    BigDecimal getEps1(String stockCode);
    @Select("SELECT YEAR2 FROM predict WHERE STOCK_CODE = #{stockCode}")
    Integer getYear2(String stockCode);
    @Select("SELECT EPS2 FROM predict WHERE STOCK_CODE = #{stockCode}")
    BigDecimal getEps2(String stockCode);
    @Select("SELECT YEAR3 FROM predict WHERE STOCK_CODE = #{stockCode}")
    Integer getYear3(String stockCode);
    @Select("SELECT EPS3 FROM predict WHERE STOCK_CODE = #{stockCode}")
    BigDecimal getEps3(String stockCode);
    @Select("SELECT YEAR4 FROM predict WHERE STOCK_CODE = #{stockCode}")
    Integer getYear4(String stockCode);
    @Select("SELECT EPS4 FROM predict WHERE STOCK_CODE = #{stockCode}")
    BigDecimal getEps4(String stockCode);
}




